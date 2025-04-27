import React, { useState , useEffect} from 'react';
import { IoCloseCircle } from 'react-icons/io5';
import { BounceLoader } from 'react-spinners';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';

function Hero() {
    const [img, setIMG] = useState(null);
    const [loading, setLoading] = useState(false);
    const [predictedClass, setPredictedClass] = useState('');
    const [prediction, setPrediction] = useState('');
    const [name, setName] = useState('Rice');
    const [displayedPred, setDisplayedPred] = useState(''); // For typewriter effect
    const [currentIndex, setCurrentIndex] = useState(0); // Track typed characters

    const url = 'http://127.0.0.1:8000'; // Backend API URL

    const handleChange = (event) => {
        setName(event.target.value);
    };

    const handleSubmit = async () => {
        if (!img) {
            alert('Please upload an image before submitting.');
            return;
        }

        setLoading(true);
        setPrediction('');

        const formData = new FormData();
        formData.append('name', name);
        formData.append('file', img);

        try {
            const response = await fetch(`${url}/predict/`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setPredictedClass(data.predicted_class);
                setPrediction(data.response);
            } else {
                const errorData = await response.json();
                console.error('Error Response:', errorData);
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {

        if (currentIndex < prediction.length && !loading) {
            const timer = setTimeout(() => {
                setDisplayedPred(prev => prev + prediction[currentIndex]);
                setCurrentIndex(currentIndex + 1);
            }, 1); // Speed of the typewriter (in ms)
            return () => clearTimeout(timer);
        }
    }, [currentIndex, prediction, loading]);

    return (
        <div className='bg-primary w-[100vw] h-[100vh] flex justify-between'>
            <div className='w-[100%] h-full overflow-scroll flex justify-between'>
                <div className='text-white w-full flex flex-col'>
                    <div className='flex justify-between items-center px-6 py-6 mb-10'>
                        <h1 className='text-lg font-medium'>Crop Disease Prediction</h1>
                    </div>

                    {img != null ? (
                        <div className='w-full py-12 flex flex-col justify-center items-center'>
                            <div className='px-16 py-12 rounded-xl bg-layer bg-opacity-90 flex flex-col items-center justify-center'>
                                <img src={URL.createObjectURL(img)} alt="" className='w-[20vw] object-contain rounded-xl' />
                                <div className='flex justify-center items-center gap-2 mt-8'>
                                    {loading ? (
                                        <div className='flex flex-col items-center'>
                                            <BounceLoader color='#000000' />
                                            <motion.p
                                                initial={{ opacity: 0, scale: 0.5 }}
                                                whileInView={{ opacity: 1, scale: 1 }}
                                                transition={{ duration: 1 }}
                                                className='mt-4'>Predicting crop disease...
                                            </motion.p>
                                        </div>
                                    ) : (
                                        <div>
                                            <h1 className='text-white font-semibold mb-4'>Select the crop type:</h1>
                                            <select
                                                className='bg-layer rounded-lg px-4 py-3 text-white'
                                                onChange={handleChange}>
                                                <option value="Rice">Rice</option>
                                                <option value="Corn">Corn</option>
                                                <option value="Wheat">Wheat</option>
                                                <option value="Potato">Potato</option>
                                            </select>
                                            <div className='flex gap-2 mt-4'>
                                                <button
                                                    className='bg-slate-700 text-white px-5 py-2 rounded-md'
                                                    onClick={handleSubmit}>
                                                    Generate
                                                </button>
                                                <button
                                                    className='text-white'
                                                    onClick={() => { setIMG(null); setPrediction(''); }}>
                                                    <IoCloseCircle size={30} />
                                                </button>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                            {displayedPred && (
                                <div className='px-14'>
                                    <div className='w-[60vw] bg-layer bg-opacity-80 rounded-3xl mt-8 px-8 py-6'>
                                        <h1 className='text-2xl font-semibold text-white mb-4'>{predictedClass}</h1>
                                        <ReactMarkdown className='text-white'>{displayedPred}</ReactMarkdown>
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        <motion.div
                            initial={{ y: '-100vh', opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            transition={{ duration: 0.5, type: 'spring', stiffness: 120, damping: 20 }}
                            className='w-full flex flex-col justify-center items-center'>
                            <div className='text-slate-900 w-[50vw] h-[10vh] bg-white bg-opacity-90 rounded-sm flex items-center gap-2 px-4'>
                                <input
                                    type="file"
                                    className='custom-file-input'
                                    onChange={(event) => setIMG(event.target.files[0])} />
                                <p className='text-xs text-gray-500'>Upload an image file</p>
                            </div>
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Hero;
